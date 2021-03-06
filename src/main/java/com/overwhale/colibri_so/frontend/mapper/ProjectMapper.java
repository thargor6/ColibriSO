package com.overwhale.colibri_so.frontend.mapper;

import com.overwhale.colibri_so.backend.entity.Project;
import com.overwhale.colibri_so.frontend.dto.ProjectDto;
import org.mapstruct.Mapper;

@Mapper
public interface ProjectMapper {
  Project dtoToEntiy(ProjectDto dto);

  ProjectDto entityToDto(Project entity);
}
