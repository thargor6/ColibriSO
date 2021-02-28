package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.frontend.dto.IntentDto;
import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.frontend.mapper.IntentMapper;
import com.overwhale.colibri_so.backend.repository.IntentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class IntentService extends CrudService<IntentDto, UUID>  {
  private final IntentRepository repository;

  public IntentService(@Autowired IntentRepository repository) {
    this.repository = repository;
  }

  public IntentDto update(IntentDto dto) {
    Intent entity = IntentMapper.INSTANCE.dtoToEntiy(dto);
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    } else {
      entity.setLastChangedTime(OffsetDateTime.now());
    }
    return IntentMapper.INSTANCE.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<IntentDto, UUID> getRepository() {
    return null;
  }

  public Optional<IntentDto> get(UUID id) {
    return repository.findById(id).map( e -> IntentMapper.INSTANCE.entityToDto(e) );
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<IntentDto> list(Pageable pageable) {
    return repository.findAll(pageable).map( e -> IntentMapper.INSTANCE.entityToDto(e) );
  }

  public int count() {
    return (int)repository.count();
  }
}
