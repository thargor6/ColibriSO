package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.backend.repository.UserRepository;
import com.overwhale.colibri_so.frontend.dto.UserDto;
import com.overwhale.colibri_so.frontend.mapper.UserMapper;
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
public class UserService extends CrudService<UserDto, UUID> {
  private final UserRepository repository;
  private final UserMapper userMapper;

  public UserService(@Autowired UserRepository repository, UserMapper userMapper) {
    this.repository = repository;
    this.userMapper = userMapper;
  }

  public UserDto update(UserDto dto) {
    User entity = userMapper.dtoToEntiy(dto);
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    }
    entity.setLastChangedTime(OffsetDateTime.now());
    return userMapper.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<UserDto, UUID> getRepository() {
    return null;
  }

  public Optional<UserDto> get(UUID id) {
    return repository.findById(id).map(e -> userMapper.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<UserDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> userMapper.entityToDto(e));
  }

  public UserDto getByUsername(String username) {
    return userMapper.entityToDto(repository.getByUsername(username));
  }

  public int count() {
    return (int) repository.count();
  }
}
