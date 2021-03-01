package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.Project;
import com.overwhale.colibri_so.backend.repository.ProjectRepository;
import com.overwhale.colibri_so.frontend.dto.ProjectDto;
import com.overwhale.colibri_so.frontend.mapper.ProjectMapper;
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
public class ProjectService extends CrudService<ProjectDto, UUID> {
  private final ProjectRepository repository;

  public ProjectService(@Autowired ProjectRepository repository) {
    this.repository = repository;
  }

  public ProjectDto update(ProjectDto dto) {
    Project entity = ProjectMapper.INSTANCE.dtoToEntiy(dto);
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    }
    entity.setLastChangedTime(OffsetDateTime.now());
    return ProjectMapper.INSTANCE.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<ProjectDto, UUID> getRepository() {
    return null;
  }

  public Optional<ProjectDto> get(UUID id) {
    return repository.findById(id).map(e -> ProjectMapper.INSTANCE.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<ProjectDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> ProjectMapper.INSTANCE.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
